let icon = document.querySelector('.hamburger');
let menu = document.querySelector('.menu');
let one = document.querySelector('.one');
let two = document.querySelector('.two');
let three = document.querySelector('.three');


let open = () => {
    one.style.transform = 'rotate(45deg)';
    two.style.transform = 'rotate(-45deg)';
    one.style.top = '12px';
    two.style.top = '12px';
    three.style.top = '24px';
    three.style.opacity = '0';

    menu.style.transform = 'translateX(0)';

    icon.classList.remove('closed');
    icon.classList.add('open');
    
    icon.removeEventListener('click', open);
    icon.addEventListener('click', close);
};

let close = () => {
    one.style.transform = 'rotate(0)';
    two.style.transform = 'rotate(0)';

    three.style.opacity = '1';
  
    one.style.top = '0';
    two.style.top = '12px';
    three.style.top = '24px';

    menu.style.transform = 'translateX(100%)';

    icon.classList.remove('open');
    icon.classList.add('closed');
  
    icon.removeEventListener('click', close);
    icon.addEventListener('click', open);
};


if(icon.classList.contains('closed')){
    icon.addEventListener('click', open);
} else {
    icon.addEventListener('click', close);
}