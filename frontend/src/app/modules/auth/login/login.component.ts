import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
  email = '';
  password = '';
  errorMessage = '';

  constructor(
    private router: Router,
    private authService: AuthService,
  ) {}

  ngOnInit(): void {
    if (localStorage.getItem('isLoggedIn') === 'true') {
      this.router.navigate(['/dashboard']);
    }
  }

  login(): void {
    this.authService.login(this.email, this.password).subscribe({
      next: (response) => {
        localStorage.setItem('isLoggedIn', 'true');
        localStorage.setItem('username', response.username);
        localStorage.setItem('role', response.role);

        this.router.navigate(['/dashboard']);
      },

      error: () => {
        this.errorMessage = 'Invalid Username or Password';
        alert(this.errorMessage);
      },
    });
  }
}
