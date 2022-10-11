document.addEventListener('DOMContentLoaded', function() {
    const purchased = document.querySelector('div.purchased button');
    const purchase = document.querySelectorAll('div.available_prizes div.this_prize div.card button');

    purchase.forEach(element => {
        element.addEventListener('click', () => {
            purchase_prize(element.id, element);
        });
    });

    purchased.addEventListener('click', () => {get_purchased()});
});

function get_purchased() {
    const user_id = document.querySelector('span#user_id').getAttribute('value');
    const purchased_list = document.querySelector('div.purchased');
    let for_now = purchased_list.innerHTML;
    let output = ``;

    purchased_list.innerHTML = `
    
    <button class="btn btn-primary" type="button" 
        style="position: relative;
        left: -50%;
        transform: translate(50%);" disabled>
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        در حال لود شدن...
    </button>

    `;

    fetch(`api/prizes_got/${user_id}`,{
        method: 'GET'
    })
    .then(response => response.json())
    .then(result => {
        result.result.forEach(purchase => {
            output += `
                <a class="list-group-item list-group-item-action" style="cursor: pointer;">
                    <h6 class="mb-1">${purchase.name}</h6>
                    <p style="font-size: smaller;" class="mb-1">متن کد: <b>${purchase.code}</b></p>
                </a>
            `;
        });

        if (output === ``) {purchased_list.innerHTML = "<p>شما جایی ثبت‌نام نکرده‌اید.</p>"; return;}

        purchased_list.innerHTML = `
            <h5>لیست موارد ثبت‌نام شده</h5><br>
            <div class="list-group">
                ${output}
            </div>
        `;

        const all_links = document.querySelectorAll('div.purchased a');
        all_links.forEach(link => {
            link.addEventListener('click', () => {
                let code = link.children[1].children[0].innerHTML;
                navigator.clipboard.writeText(code);
                window.alert('کد مورد نظر در کلیپ‌ بورد ذخیره شد.');
            });
        });
    });
}

function purchase_prize(prize_id, button) {
    const alertplace = document.querySelector(`div[class="this_prize ${prize_id}"]`);
    const currentscore = document.querySelector('b#current_score');
    const score_needed = alertplace.children[0].children[1].children[0];

    button.disabled = true;
    alertplace.style.cursor = 'wait';

    if (parseInt(score_needed.innerHTML) > parseInt(currentscore.innerHTML)) {
        alert("شما به اندازه کافی امتیاز ندارید.", "warning", alertplace); return;
    }

    fetch(`api/buy_prize/${prize_id}`,{
        method: 'POST',
        headers: { "X-CSRFToken": csrftoken }
    })
    .then(response => response.json())
    .then(result => {
        if (result['result'] === "You Don't have enough score.") {alert("شما به اندازه کافی امتیاز ندارید.", "warning", alertplace); alertplace.style.cursor = ''; return;}
        if (result['result'] === "You should be logged in.") {alert("شما از حساب کاربری خود خارج شده‌اید.", "danger", alertplace); alertplace.style.cursor = ''; return;}
        if (result['result'] === "You have already bought this prize.") {alert("شما قبلا این را خریداری کرده‌اید.", "danger", alertplace); alertplace.style.cursor = ''; return;}
        
        currentscore.innerHTML = parseInt(currentscore.innerHTML) - parseInt(score_needed.innerHTML);

        if (result['result'] === "Successfuly saved the result.") {alert("خرید با موفقیت انجام شد.", "success", alertplace); alertplace.style.cursor = ''; return;}
    });
}