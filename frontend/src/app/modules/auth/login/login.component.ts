import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  email: string = '';
  password: string = '';
  errorMessage = '';

  constructor(private router: Router) {}

  ngOnInit(): void {

    // ✅ If already logged in, redirect to dashboard
    if (localStorage.getItem('isLoggedIn') === 'true') {
      this.router.navigate(['/dashboard']);
    }

  }

  login(): void {

    // ✅ Multiple users
    const users = [
      {
        email: 'bagla@gmail.com',
        password: 'bagla@123'
      },
      {
        email: 'admin@gmail.com',
        password: 'admin123'
      },
      {
        email: 'BGLIIN',
        password: 'bgliin@123'
      }
    ];

    // ✅ Check credentials
    const validUser = users.find(
      user =>
        user.email === this.email &&
        user.password === this.password
    );

    if (validUser) {

      // ✅ Store login state
      localStorage.setItem('isLoggedIn', 'true');
      localStorage.setItem('user', validUser.email);

      // ✅ Redirect to dashboard
      this.router.navigate(['/dashboard']);

    } else {

      this.errorMessage = 'Invalid credentials';
      alert('Wrong email or password');

    }
  }
}
