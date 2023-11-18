window.onload = function() {
    fetch('http://127.0.0.1:8000/boards')
      .then(response => response.json())
      .then(data => {
        let sidebarList = document.querySelector('.sidebar ul');
        data.forEach(board => {
          let listItem = document.createElement('li');
          let link = document.createElement('a');
          link.href = `boardYandex.html`;
          link.textContent = board.title;
          listItem.appendChild(link);
          sidebarList.appendChild(listItem);
        });
      })
      .catch(error => {
        console.error('Ошибка:', error);
      });
  };
  