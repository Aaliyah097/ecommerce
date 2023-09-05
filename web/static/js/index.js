const catalog_button = document.getElementById('catalog_block')
const categoryName = document.getElementById("category-list");
const categoryChildren = document.getElementById("category-children");

let data = [
  {
      "name": "Категория 1",
      "slug": "cat-1",
      "children": [
          {
              "name": "Категория 2",
              "slug": "cat-1-cat-2",
              "children": [
                  {
                      "name": "Категория 3",
                      "slug": "cat-1-cat-1-cat-2-cat-3",
                      "children": []
                  }
              ]
          },
          {
              "name": "Категория 4",
              "slug": "cat-1-cat-4",
              "children": []
          },
          {
              "name": "Категория 6",
              "slug": "cat-1-cat-1-cat-4",
              "children": []
          }
      ]
  },
  {
    "name": "Категория 1",
    "slug": "cat-1",
    "children": [
        {
            "name": "Категория 2",
            "slug": "cat-1-cat-2",
            "children": [
                {
                    "name": "Категория 3",
                    "slug": "cat-1-cat-1-cat-2-cat-3",
                    "children": []
                }
            ]
        },
        {
            "name": "Категория 4",
            "slug": "cat-1-cat-4",
            "children": []
        },
        {
            "name": "Категория 6",
            "slug": "cat-1-cat-1-cat-4",
            "children": []
        }
    ]
},
{
  "name": "Категория 1",
  "slug": "cat-1",
  "children": [
      {
          "name": "Категория 2",
          "slug": "cat-1-cat-2",
          "children": [
              {
                  "name": "Категория 3",
                  "slug": "cat-1-cat-1-cat-2-cat-3",
                  "children": []
              }
          ]
      },
      {
          "name": "Категория 4",
          "slug": "cat-1-cat-4",
          "children": []
      },
      {
          "name": "Категория 6",
          "slug": "cat-1-cat-1-cat-4",
          "children": []
      }
  ]
},
{
  "name": "Категория 1",
  "slug": "cat-1",
  "children": [
      {
          "name": "Категория 2",
          "slug": "cat-1-cat-2",
          "children": [
              {
                  "name": "Категория 3",
                  "slug": "cat-1-cat-1-cat-2-cat-3",
                  "children": []
              }
          ]
      },
      {
          "name": "Категория 4",
          "slug": "cat-1-cat-4",
          "children": []
      },
      {
          "name": "Категория 6",
          "slug": "cat-1-cat-1-cat-4",
          "children": []
      }
  ]
},
{
  "name": "Категория 1",
  "slug": "cat-1",
  "children": [
      {
          "name": "Категория 2",
          "slug": "cat-1-cat-2",
          "children": [
              {
                  "name": "Категория 3",
                  "slug": "cat-1-cat-1-cat-2-cat-3",
                  "children": []
              }
          ]
      },
      {
          "name": "Категория 4",
          "slug": "cat-1-cat-4",
          "children": []
      },
      {
          "name": "Категория 6",
          "slug": "cat-1-cat-1-cat-4",
          "children": []
      }
  ]
}
];
catalog_button.addEventListener('click', () => {
  axios.get('/catalog/categories/')
    .then(response => {
      // let data = response.data
      displayCategories(categoryName, data);
     

    }).catch(error => {
      console.log(error)
    })

  let icon = document.getElementById('nav-icon3')
  icon.classList.toggle('open')
  let close = document.querySelector('.catalog_menu_close')
  close.classList.toggle('catalog_menu_open')
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


function displayCategories(categoryList, categories) {
  categoryList.innerHTML = ""; // Очищаем содержимое

  function displayCategory(category, parentElement) {
      const categoryItem = document.createElement("p");
      categoryItem.textContent = category.name;
      parentElement.appendChild(categoryItem);

      // Создаем список вложенных элементов
      const childList = document.createElement("ul");
      parentElement.appendChild(childList);
      childList.classList.add("hidden");

      // Добавляем обработчик события на клик
      categoryItem.addEventListener("click", () => {
        console.log(categoryItem, childList)
          // Переключаем класс "hidden" для скрытия/показа как <ul>, так и <li>
          childList.classList.toggle("hidden");
      });

      // Добавляем дочерние элементы (рекурсивно)
      category.children.forEach(child => {
          const listItem = document.createElement("li");
          listItem.textContent = child.name;
          childList.appendChild(listItem);
          listItem.classList.add("hidden");
          categoryItem.addEventListener('click', () => {
            listItem.classList.toggle("hidden");
          })
         

          // Если есть дочерние категории, выводим их
          if (child.children.length > 0) {
              displayCategory(child, listItem);
          }
      });
  }

  // Выводим категории на первом уровне
  categories.forEach(category => {
      displayCategory(category, categoryList);
  });
}
