var menu = document.querySelector('.nav__list');
var burger = document.querySelector('.burger');
var doc = $(document);
var l = $('.scrolly');
var panel = $('.panel');
var vh = $(window).height();



var openMenu = function() {
  burger.classList.toggle('burger--active');
  menu.classList.toggle('nav__list--active');
};

// reveal content of first panel by default
panel.eq(0).find('.panel__content').addClass('panel__content--active');




var init = function() {
  burger.addEventListener('click', openMenu, false);
  
};

doc.on('ready', init);


function nav(p) {
	if(p == 1){
		document.cookie = "nav=1";
		document.getElementById("f1").style.display = 'block';
		document.getElementById("f").style.display = 'none';
	}
	if(p == 2){
		document.cookie = "nav=2";
		document.getElementById("f").setAttribute("src", "App/streamsummary/streamsummary.html");
		document.getElementById("f1").style.display = 'none';
		document.getElementById("f").style.display = 'block';

	}
	if(p == 3){
		document.cookie = "nav=3";
		document.getElementById("f").setAttribute("src", "App/streamstatistics/streamstatistics.html");
		document.getElementById("f1").style.display = 'none';
		document.getElementById("f").style.display = 'block';

	}
	if(p == 4){
		document.cookie = "nav=4";
		document.getElementById("f").setAttribute("src", "App/About/About.html");
		document.getElementById("f1").style.display = 'none';
		document.getElementById("f").style.display = 'block';

	}
	if(p == 5){
		document.cookie = "nav=5";
		var obj = JSON.parse(localStorage.getItem('myStorage'));
		obj['logged'] = false;
		localStorage.setItem('myStorage', JSON.stringify(obj));
	}
	if(p == 6)
	{
		document.cookie = "nav=6";
		document.getElementById("f").setAttribute("src", "App/settings/settings.html");
		document.getElementById("f1").style.display = 'none';
		document.getElementById("f").style.display = 'block';

	}
}