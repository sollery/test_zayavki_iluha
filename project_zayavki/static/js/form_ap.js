   let birdForm = document.querySelectorAll(".div_form")
        let container = document.querySelector("#form-container")
        let addButton = document.querySelector("#add-form")
        let totalForms = document.querySelector("#id_form-TOTAL_FORMS")

        let formNum = birdForm.length-1

        addButton.addEventListener('click', addForm)


        function addForm(e){
            e.preventDefault()
            let newForm = birdForm[0].cloneNode(true)
            let formRegex = RegExp(`form-(\\d){1}-`,'g')
            formNum++
            newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
            container.insertBefore(newForm, addButton)
            totalForms.setAttribute('value', `${formNum+1}`)

       }


const text = document.querySelector('.text');
const btn_form = document.querySelector('.btn_form');

btn_form.addEventListener('click', () => {
    btn_form.style.display = 'none';
    addButton.style.display = 'none';
    text.style.display = 'block';
});

