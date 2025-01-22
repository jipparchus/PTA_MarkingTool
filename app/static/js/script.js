
document.addEventListener("DOMContentLoaded", () => {
    // For navigation tab
    // the box containing the link for the tabs
    const boxs = document.querySelectorAll(".box");
    const currentPath = window.location.pathname;

    // check the path of the link included in each box
    boxs.forEach(box => {
        // a-tag within the box(p-tag)
        const link = box.querySelector("a");
        // if the link == current path
        if (link && link.getAttribute("href") === currentPath) {
            // add 'current' attribute
            box.classList.add("current");
            link.classList.add("current");
        } else {
            // remove 'current' attribute
            box.classList.remove("current");
        }
    });

    // var selected = document.querySelector('[selected=""]');
    // selected.classList.add('highlight_row')

    // console.log(selected)

    // For table highlight
    // Dropdown selectors
    var select_id = document.getElementsByName( "sub_id_selected" )[0];
    var select_cp = document.getElementsByName( "point_selected" )[0];
    // Tables
    var tables = document.querySelectorAll(".dataframe");
    
    select_id.addEventListener('click', () => {
        const id_selected = select_id.selectedOptions[0];
        console.log(id_selected);
        // Highlight the row with the selected submission id
        tables.forEach(table => {
            // Rows including the row head
            var tr = table.getElementsByTagName('TR');
            // Heads including row head
            var th = table.getElementsByTagName('TH');
            const ncols = tr[1].getElementsByTagName('TD').length;
            const row_heads = Object.entries(th).slice(ncols+1).map(entry => entry[1]);
            console.log(row_heads)
            for(var i = 0; i < tr.length; i++){
                // Array of cells in the row excluding row head
                var td = tr[(i+1)].getElementsByTagName('TD');
                // If selected id matches i-th row_heads value, highlight.
                if(row_heads[i].innerHTML == id_selected.value){
                    for(var j = 0; j < td.length; j++){td[j].classList.add('highlight_row')}
                }
                else{
                    for(var j = 0; j < td.length; j++){td[j].classList.remove('highlight_row')}
                }
                
            }
        });
    });
    select_cp.addEventListener('click', () => {
        const cp_selected = select_cp.selectedOptions[0];
        console.log(cp_selected);
        // Highlight the row with the selected checkpoint
        tables.forEach(table => {
            // Rows including the row head
            var tr = table.getElementsByTagName('TR');
            // Heads including row head
            var th = table.getElementsByTagName('TH');
            const ncols = tr[1].getElementsByTagName('TD').length;
            // var tr = table.getElementsByTagName('TR');
            const col_heads = Object.entries(th).slice(1, ncols+1).map(entry => entry[1]);
            // For each row's j-th column cell add class highlight
            for(var i = 0; i < tr.length; i++){
                var td = tr[i].getElementsByTagName('TD');
                for(var j = 0; j < td.length; j++){
                    if(col_heads[j].innerHTML == cp_selected.value){td[j].classList.add('highlight_col')}
                    else{td[j].classList.remove('highlight_col')}
                }
            }
        });
    });


});


