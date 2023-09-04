const catalog_button = document.getElementById('catalog_block')
catalog_button.addEventListener('click', ()=> {
	let icon = document.getElementById('nav-icon3')
	icon.classList.toggle('open')
})

const navMenu = document.querySelector('.pages');
const links = navMenu.querySelectorAll('a');

links.forEach(link => {
  link.addEventListener('click', (event) => {
    event.preventDefault();

    links.forEach(otherLink => {
      otherLink.classList.remove('active_link_button');
    });

    link.classList.add('active_link_button');
  });
});