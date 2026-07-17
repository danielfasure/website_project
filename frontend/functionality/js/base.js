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
                const response = await fetch(`/admin/add_library`, {
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
                const response = await fetch(`/admin/add_book?library=${libraryid}`, {
    method: "POST",
    credentials: "include",
    headers: {
        "Content-Type": "application/json"
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
                    window.location.href = '/auth/library-page'; 
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

  let role_checker = document.getElementById("roles");
let code_opener = document.getElementById("enter_admin_code");

role_checker.addEventListener("change", function(){

       if (role_checker.value =="admin") {
        
       code_opener.style.display = "block";
    } else {
     code_opener.style.display = "none"
     
    }

});
//load edit user page 
let load_user_edit_button = document.getElementById("load_edit_user")
    load_user_edit_button.addEventListener("click",function(){
    
            alert("helooo")
        window.location.href = `/auth/edit_user_info`;
 
    });
    

    // Register JS
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        role_checker = document.getElementById("roles");
         
        registerForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            if (data.password !== data.password2) {
                alert("Passwords do not match");
                return;
            }
            if (role_checker.value== "admin"){
         
            
          const role_input_checker = document.querySelector('[name="admin_pin"]')
                if(parseInt(role_input_checker.value)===1234){
                    alert("accepted")
                  
                }else{
                    alert("this is not correct ")

                    return}
        }
          
            const payload = {
              email: data.email,
              username: data.username,
              first_name: data.first_name,
              last_name: data.last_name,
              role: role_checker.value,
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
                    window.location.href = "/auth/login-page";
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