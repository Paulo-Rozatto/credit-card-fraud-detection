async function get_hist(id, unixTime) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/window/${id}/${unixTime}`);
        const data = await response.json();

        const tableBody = document.querySelector('#rules-table tbody');
        tableBody.innerHTML = '';

        data.prediction_array.forEach((rule, idx) => {
            const row = document.createElement('tr');
            row.classList.add(rule.passed ? 'passed' : 'failed');

            const cellIndex = document.createElement('td');
            cellIndex.textContent = idx + 1;

            const cellStatus = document.createElement('td');
            cellStatus.textContent = rule.passed == 1 ? 'Sim' : 'Não';

            row.appendChild(cellIndex);
            row.appendChild(cellStatus);
            tableBody.appendChild(row);
        });


        // Handle SVG image
        const svgContainer = document.getElementById('svg-container');
        svgContainer.innerHTML = `<img src="${data.svg}">`;
    } catch (error) {
        console.error("Error fetching window data:", error);
    }
}

try {
    const result = await fetch('http://127.0.0.1:5000/transactions')
    const json = await result.json()

    const tableBody = document.getElementById("table-body");
    const fragment = document.createDocumentFragment();


    if (json) {
        json.forEach(([id, unixTime]) => {
            const tr = document.createElement("tr");

            const tdId = document.createElement("td");
            tdId.textContent = id;

            const tdDate = document.createElement("td");
            console.log(unixTime)
            tdDate.textContent = new Date(unixTime * 1110).toLocaleString();

            tr.appendChild(tdId);
            tr.appendChild(tdDate);
            tr.addEventListener("click", () => get_hist(id, unixTime));

            fragment.appendChild(tr);
        });

        tableBody.appendChild(fragment);
    }
}
catch (error) {
    console.error("Error fetching window data:", error);
}

