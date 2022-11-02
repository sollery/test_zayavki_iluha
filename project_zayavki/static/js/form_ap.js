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
    newForm.id = 'form-'+ String(formNum)
    newForm.hidden = false;
    var but_del = newForm.childNodes[7].childNodes[1].childNodes[6]
    newForm.childNodes[7].childNodes[1].childNodes[6].dataset.prefix = 'form-'+ String(formNum)
    newForm.childNodes[7].childNodes[1].childNodes[4].childNodes[0].checked = false
    container.insertBefore(newForm, addButton)
    console.log(but_del)
    totalForms.setAttribute('value', `${formNum+1}`)
}


const text = document.querySelector('.text');
const btn_form = document.querySelector('.btn_form');

btn_form.addEventListener('click', () => {
    btn_form.style.display = 'none';
    addButton.style.display = 'none';
    text.style.display = 'block';
});


//
//const count_s = document.querySelector('#id_form-1-count_employee').value;
//console.log(count_s)
const but_count_emp = document.querySelector('.count_but_e');
document.querySelector('.count_but_e');
const count_emp = document.querySelector('.count_emp');
const count_s = $('.form_count')




function emp_sum() {
  var count_s = $('.form_count')
  let sum = 0
  count_s.each(function() {
    sum += Number(this.value);
    console.log(sum)
    count_emp.innerHTML = String('Общее кол-во: ' + sum);
  })
}
but_count_emp.addEventListener('click',emp_sum)
//document.querySelector("select").addEventListener('change', function (e) {
//  console.log("Changed to: " + e.target.value)
//})




del_but.forEach((e) => {
    e.onclick = function() {
    console.log(del_but.length)
//    let a = document.querySelector('#'+e.dataset.prefix)
//    b = document.querySelector('#id_' + e.dataset.prefix + '-DELETE')
//    b.checked = true;
//    a.hidden = true;
    console.log(e)
}
})
//console.log(del_but)
//del_but.onclick = function () {
//    console.log(del_but)
//}
