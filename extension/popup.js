// Copyright 2018 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// 'use strict';

// let changeColor = document.getElementById('changeColor');

// chrome.storage.sync.get('color', function(data) {
//   changeColor.style.backgroundColor = data.color;
//   changeColor.setAttribute('value', data.color);
// });

// changeColor.onclick = function(element) {
//   let color = element.target.value;
//   chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
//     chrome.tabs.executeScript(
//         tabs[0].id,
//         {code: 'document.body.style.backgroundColor = "' + color + '";'});
//   });
// };

// Helper Method to 
var button = document.createElement('button');

async function generateList(){
   // Performs initial fetch to get the database
   let res = await getList();
   // if the database is empty then we create an import button
   if (res.length == 0){
      generateImportButton();
   }
   else {
      //if not empty then we populate the list 
      createList(res)
   }
}

function getList(){
   return fetch('http://localhost:5000/issues')
      .then( res => res.json())
      .catch(err => console.log(err))
}

function generateImportButton(){
   button.id = "mybutton";
   button.innerText = "import"
   document.body.appendChild(button);
   var butt = document.getElementById('mybutton');
   butt.addEventListener('click', importDatabase);
}

// Generate a list of ul elements
function createList(databaseElems){
   var list = document.createElement('ui');
   list.id = "my_list";
   for(var i = 0; i < databaseElems.length; i++){
      var item = document.createElement('li');

      // Register click event so we can delete it from the list
      item.addEventListener('click', function(event) {
         listItem = event.target;
         //delete from database
         id = listItem.innerText.split(" ")[1];
         fetch('http:localhost:5000/delete?id=' + id , {method: 'POST'})
            .then(res => {
               listItem.remove()
            })
      });

      item.appendChild(document.createTextNode(databaseElems[i].title + " " +  databaseElems[i].id));
      list.appendChild(item);
   }
   document.body.appendChild(list)
}

function deleteListElement(){

}

async function importDatabase() {
   await fetch('http://localhost:5000/import', {method: 'POST'})
   //remove the import button
   generateList() 
}


generateList();

