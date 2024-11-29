const result = await fetch('http://127.0.0.1:5000/transactions')
const json = await result.json()
console.log(json)

const tableBody = document.getElementById("table-body");
const fragment = document.createDocumentFragment();

async function get_hist(id, unixTime) {
    console.log('oi')
    const result = await fetch(`http://127.0.0.1:5000/window/${id}/${unixTime}`);
    const json = await result.json()
    console.log(json)
}

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