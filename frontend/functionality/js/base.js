 //load library

const add_library= document.getElementById('add_library')  
if (add_library){
    add_library.addEventListener('submit', async function(event){
             event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

        
            const payload = {
                name: data.name,
                postcode:data.postcode,
                capacity:data.capacity               
            };
              try {
                const response = await fetch(`/lib/add_library`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${getCookie('access_token')}`
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    form.reset(); // Clear the form
                } else {
                    // Handle error
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
               }
        });

        
    }



  

 //load library
 const load_library =document.getElementById('load_library');
if(load_library){
    load_library.addEventListener('click',async function() {
        window.location.href = `/lib/load-library-add`  
        
    });
  
}





//addbook
const add_book= document.getElementById('add_books')  
if (add_book){
    add_book.addEventListener('submit', async function(event){
             event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            const button = document.getElementById('addbook');
            const libraryid = button.dataset.library;

            const payload = {
                book_name: data.book_name,
                book_author:data.book_author               
            };
              try {
                const response = await fetch(`/book/addbook/?library=${libraryid}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${getCookie('access_token')}`
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    form.reset(); // Clear the form
                } else {
                    // Handle error
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
               }
        });

        
    }


  
  
  //load books
const load_books= document.getElementById('loadbook');
if (load_books){


    load_books.addEventListener('click',async function (){
       const libraryid = this.value;
       window.location.href =  `/book/add_book/?library=${libraryid}`;
    });
}
   

//loan books
const loan_books= document.getElementById('loanbook');
if(loan_books){
    loan_books.addEventListener('click',  async function () {

        const selectedBooks = [];

        document.querySelectorAll('.book_selector:checked').forEach(box => {
            selectedBooks.push(box.value);
        });
         if (selectedBooks.length === 0) {
        alert("No books selected");
        return;
    }
 try {
        for (const bookId of selectedBooks) {

            const response = await fetch(`/book/loanbook/${bookId}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${getCookie('access_token')}`
                }
            });

            if (!response.ok) {
                const error = await response.json();
                console.error(`Book ${bookId} failed:`, error.detail);
            }
        }

        // refresh after all requests finish
        location.reload();

    } catch (err) {
        console.error(err);
        alert("Something went wrong");
    }
});


        
}
   

//return books
const return_books= document.getElementById('returnbook');
if(return_books){
    return_books.addEventListener('click',  async function () {

        const returnBooks = [];

        document.querySelectorAll('.return_book_selector:checked').forEach(box => {
            returnBooks.push(box.value);
        });
         if (returnBooks.length === 0) {
        alert("No books selected");
        return;
    }
 try {
        for (const bookId of returnBooks) {

            const response = await fetch(`/book/unloanbook/${bookId}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${getCookie('access_token')}`
                }
            });

            if (!response.ok) {
                const error = await response.json();
                console.error(`Book ${bookId} failed:`, error.detail);
            }
        }

        // refresh after all requests finish
        location.reload();

    } catch (err) {
        console.error(err);
        alert("Something went wrong");
    }
});


        
}
   
   
   
   
   //entering library 
document.querySelectorAll('.select-library').forEach(btn => {
    btn.addEventListener('click', async function () {
        const libraryid = this.value;
        const response = await fetch(`/lib/load-userbook`)

        window.location.href = `/lib/book-page?library_id=${libraryid}`;
    });
});


    // Add Todo JS
    const todoForm = document.getElementById('todoForm');
    if (todoForm) {
        todoForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            const payload = {
                title: data.title,
                description: data.description,
                priority: parseInt(data.priority),
                complete: false
            };

            try {
                const response = await fetch('/todos/todo', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${getCookie('access_token')}`
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    form.reset(); // Clear the form
                } else {
                    // Handle error
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }

    // Edit Todo JS
    const editTodoForm = document.getElementById('editTodoForm');
    if (editTodoForm) {
        editTodoForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        var url = window.location.pathname;
        const todoId = url.substring(url.lastIndexOf('/') + 1);

        const payload = {
            title: data.title,
            description: data.description,
            priority: parseInt(data.priority),
            complete: data.complete === "on"
        };

        try {
            const token = getCookie('access_token');
            console.log(token)
            if (!token) {
                throw new Error('Authentication token not found');
            }

            console.log(`${todoId}`)

            const response = await fetch(`/todos/todo/${todoId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                window.location.href = '/todos/todo-page'; // Redirect to the todo page
            } else {
                // Handle error
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });

        document.getElementById('deleteButton').addEventListener('click', async function () {
            var url = window.location.pathname;
            const todoId = url.substring(url.lastIndexOf('/') + 1);

            try {
                const token = getCookie('access_token');
                if (!token) {
                    throw new Error('Authentication token not found');
                }

                const response = await fetch(`/todos/todo/${todoId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    // Handle success
                    window.location.href = "/auth/library-page"; // Redirect to the todo page
                } else {
                    // Handle error
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });

        
    }

    // Login JS
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);

            const payload = new URLSearchParams();
            for (const [key, value] of formData.entries()) {
                payload.append(key, value);
            }

            try {
                const response = await fetch('/auth/token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: payload.toString()
                });

                if (response.ok) {
                    // Handle success (e.g., redirect to dashboard)
                    const data = await response.json();
                    // Delete any cookies available
                    logout();
                    // Save token to cookie
                    document.cookie = `access_token=${data.access_token}; path=/`;
                    window.location.href = '/auth/library-page'; // Change this to your desired redirect page
                } else {
                    // Handle error
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }

    // Register JS
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            if (data.password !== data.password2) {
                alert("Passwords do not match");
                return;
            }
            
            const payload = {
              email: data.email,
              username: data.username,
              first_name: data.first_name,
              last_name: data.last_name,
              role: data.role,
              phone_number: data.phone_number,
              password: data.password
            };

           
            try {
                
                const response = await fetch('/auth', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });
                const result = await response.json();
                console.log(result);
                if (response.ok) {
                    window.location.href = "/auth/library-page";
                } else {
                    // Handle error
                    const errorData = await response.json();
                    alert(`Error: ${errorData.message}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }
     console.log("NEW REGISTER JS LOADED");

   


    // Helper function to get a cookie by name
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    function logout() {
        // Get all cookies
        const cookies = document.cookie.split(";");
    
        // Iterate through all cookies and delete each one
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i];
            const eqPos = cookie.indexOf("=");
            const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
            // Set the cookie's expiry date to a past date to delete it
            document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
        }
    
        // Redirect to the login page
        window.location.href = '/auth/login-page';
    };