document.addEventListener('DOMContentLoaded', function() {
    const pass_form = document.querySelector('form#change_password');
    const change_button = document.querySelector('form#change_password div#input');

    pass_form.onsubmit = () => {
        change_vis(change_button, 0);

        fetch('/api/change_password', {
            method: 'POST',
            headers: { "X-CSRFToken": csrftoken },
            body: JSON.stringify({
                this_pass: pass_form.children[3].children[0].value,
                new_pass: pass_form.children[4].children[0].value,
                confirm: pass_form.children[5].children[0].value 
            })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            if (result.result === "Passwords are different.") {alert("رمزعبورهای وارد شده یکی نیستند.", "warning", pass_form); change_vis(change_button, 1);};
            if (result.result === "Password is incorrect.") {alert("رمزعبور وارد شده صحیح نیست.", "danger", pass_form); change_vis(change_button, 1);};
            if (result.result === "Password successfuly changed.") {alert("رمزعبور با موفقیت عوض شد.", "success", pass_form); location.reload();};
        });

        return false;
    };
});


function change_vis(el, vis) {
    if (vis === 0)
    {
        el.children[0].style.display = 'none';
        el.children[1].style.display = 'block';
    } else if (vis === 1) {
        el.children[0].style.display = 'block';
        el.children[1].style.display = 'none';
    }
}