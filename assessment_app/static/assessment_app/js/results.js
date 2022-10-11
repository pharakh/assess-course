var barColors = ["green", "lightgreen", "yellow", "orange", "red"];
var selected_div = undefined;

document.addEventListener('DOMContentLoaded', function() {
    const getresults = document.querySelector('button.term_selector');
    const dropdownElement = document.querySelector('select.term_selector');

    getresults.addEventListener('click', () => {getanswers(dropdownElement)});

    Chart.defaults.global.legend.display = false;
});

function getanswers(dropdownElement) {
    const term_id = dropdownElement.value;
    if (term_id === 'disabled') return;

    const all_terms = document.querySelectorAll(`div[class="gotanswer_type"]`);

    all_terms.forEach(term_show => {term_show.style.display = 'none';});

    const cur_placeholder = document.querySelector(`div[id="results ${term_id}"]`);

    // if there are already results, don't fetch anything just show what was hidden
    if (cur_placeholder.innerHTML !== '') {
        cur_placeholder.style.display = 'block';
    };

    cur_placeholder.setAttribute('class', 'gotanswer_type');

    cur_placeholder.innerHTML = `
    
    <button class="btn btn-primary" type="button" 
        style="position: relative;
        top: 30px;
        left: -50%;
        transform: translate(50%, 50%);" disabled>
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        در حال لود شدن...
    </button>

    `;

    fetch(`api/assess/${term_id}`,{
        method: 'GET'
    })
    .then(response => response.json())
    .then(result => {
        console.log(result.isTA)

        table_rows = ``;
        subjects_results = ``;
        total_results = ``;

        result.result.forEach(course => {
            this_answers = ``;
            table_rows += `
                            <tr>
                                <td>${ course.name }</td>
                                <td>${ course.answered }</td>
                            </tr>
                        `

            course.q_a.forEach(que => {
                let answers = '';
                let this_table_rows = '';

                if (que.type === "OPEN") {
                    que.ans.forEach(anser => {
                        answers += `<p>
                                        >>> ${anser}
                                    </p>
                                    <br>
                                    `;
                    });
                    this_answers += `
                    <div class="que_result">
                        <p><strong>سوال باز</strong> ${que.text}</p>
                        ${answers}
                    </div>
                    `;
                }
                else if (que.type === "CLOSE") {
                    let xValues = [];
                    let yValues = [];

                    for (const ans in que.ans) {
                        xValues.push(ans);
                        yValues.push(que.ans[ans]);

                        this_table_rows += `
                            <tr>
                                <td>${ ans }</td>
                                <td>${ que.ans[ans] }</td>
                            </tr>
                        `;
                    }

                    answers = `
                    <table class="table table-striped table-bordered">
                        <thead>
                            <tr>
                                <th scope="col">گزینه</th>
                                <th scope="col">تعداد</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${this_table_rows}
                        </tbody>
                    </table>
                    <br><br>
                    <canvas id="${course.id} ${que.id}" style="width:100%;max-width:400px;margin:auto;"></canvas>
                    <br><br>
                    `;

                    this_answers += `
                    <div class="que_result">
                        <p><strong>سوال بسته</strong> ${que.text}</p>
                        <div class="closed_results">
                            ${answers}
                        </div>
                    </div>
                    `;
                }
            });

            let course_color = `info`;
            let course_ta = ``;

            if (!result.isTA) {
                if (course.isTA) {
                    course_color = `danger`;
                    course_ta = `: «${course.nameTA}»`;
                }
            }

            subjects_results += `
            <div class="text-bg-${course_color} p-3 course_name">${ course.name } ${ course_ta }</div>
            <hr class="text-info bg-dark">
            ${this_answers}
            <hr class="text-info bg-dark">
            `
        });

        placeholder = `
            <hr>
            <div class="text-bg-primary p-3">دروس این ترم</div>
            <br>
            <table class="table table-striped table-bordered">
                <thead>
                    <tr>
                        <th scope="col">نام درس</th>
                        <th scope="col">شرکت کرده</th>
                    </tr>
                </thead>
                <tbody>
                    ${table_rows}
                </tbody>
            </table>
            <hr>
            ${subjects_results}
        `;

        cur_placeholder.innerHTML = placeholder;

        result.result.forEach(course => {
            course.q_a.forEach(que => {
                if (que.type === "CLOSE") {
                    let xValues = [];
                    let yValues = [];

                    for (const ans in que.ans) {
                        xValues.push(ans);
                        yValues.push(que.ans[ans]);
                    }
                    
                    new Chart(`${course.id} ${que.id}`, {
                        type: "doughnut",
                        data: {
                        labels: xValues,
                        datasets: [{
                            backgroundColor: barColors,
                            data: yValues
                        }]
                        },
                    });
                }
            });
        });
    })
}