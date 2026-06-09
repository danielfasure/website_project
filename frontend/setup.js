
let count = 0;
let a = '3';
let b = '8';

alert("a is " + a+" and b is "+b+" combined they are "+int(a+b));

function increase() {
    count++;
    document.getElementById("count").innerText = count;
    alert("value increased");       
}

function decrease() {
    count--;
    document.getElementById("count").innerText = count;
}