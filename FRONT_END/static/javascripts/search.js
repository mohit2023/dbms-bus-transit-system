const tableContainer = document.querySelector('.table');
const filter = document.getElementById('filter-table');

function filterTable(evt) {
    const posts = tableContainer.querySelectorAll('.row-data');
    const value = evt.target.value.toUpperCase();
    if(!(value.trim().length >= 0)){
        return ;
    }
    posts.forEach(post => {
        const x = post.querySelector('.filter-col').innerText
        const bus = x.toUpperCase();

        if(value=="" || bus.indexOf(value) > -1){
            post.style.display = 'table-row';
        }
        else{
            post.style.display = 'none';
        }
    });
}

filter.addEventListener('input',filterTable);