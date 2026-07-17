import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class AuthGuard implements CanActivate {
  constructor(private router: Router) {}

  canActivate(): boolean {
    const loggedIn = localStorage.getItem('isLoggedIn');

    if (loggedIn === 'true') {
      return true;
    }

    this.router.navigate(['/auth/login']);

    return false;
  }
}
