const siteUrl = '//127.0.0.1:8000/';
const styleUrl = siteUrl + 'static/css/bookmarklet.css';
// букмарклет будет захватывать изображения размером не менее 250x250px
const minWidth = 200;
const minHeight = 200;

// загрузка CSS
// этот код сгенерирует объект, эквивалентный тому, что создает следующий код:
// <link rel="stylesheet" type="text/css" href= "//127.0.0.1:8000/static/css/bookmarklet.css?r=1234567890123456">
var head = document.getElementsByTagName('head')[0]; // извлекли все элементы с тегом head
var link = document.createElement('link'); //создали элемент <link>
link.rel = 'stylesheet';
link.type = 'text/css';
link.href = styleUrl + '?r=' + Math.floor(Math.random()*9999999999999999);
head.appendChild(link); // добавили настроенный элемент <link> в <head> html страницы

// загрузка HTML
var body = document.getElementsByTagName('body')[0];
boxHtml = '<div id="bookmarklet"><a href="#" id="close">&times;</a><h1>Select an image to bookmark:</h1><div class="images"></div> </div>';
body.innerHTML += boxHtml;


function bookmarkletLaunch() {
    bookmarklet = document.getElementById('bookmarklet');
    var imagesFound = bookmarklet.querySelector('.images');

    imagesFound.innerHTML = ''; //очистили найденные изображения
    bookmarklet.style.display = 'block'; //отобразили
    // событие закрытия
    bookmarklet.querySelector('#close').addEventListener('click', function (){
        bookmarklet.style.display = 'none'
    });

    // ищем все элементы <img>, аттрибуты src которых заканчиваются на .jpg, .jpeg, .png
    images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]');
    images.forEach(image=>{
        console.log(image.width, image.height);
        if (image.width >= minWidth && image.height >= minHeight) {
            var imageFound = document.createElement('img');
            imageFound.src = image.src;
            imagesFound.append(imageFound);
        }
    })

    //выбор изображения
    imagesFound.querySelectorAll('img').forEach(image=>{
        image.addEventListener('click', function (event){
            imageSelected = event.target;
            bookmarklet.style.display = 'none';
            window.open(siteUrl + 'images/create/?url='
                + encodeURIComponent(imageSelected.src)
                + '&title='
                + encodeURIComponent(document.title),
                '_blank');
        })
    })
}

bookmarkletLaunch();