import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  constructor(private readonly router: Router) {}

  nowTime: string = '';
  nowDate: string = '';

  ngOnInit(): void {
    this.updateDateTime();

    // update every second
    setInterval(() => {
      this.updateDateTime();
    }, 1000);
  }

  updateDateTime(): void {
    const now = new Date();

    // India Time
    this.nowTime = now.toLocaleTimeString('en-IN', {
      timeZone: 'Asia/Kolkata',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    });

    // India Date
    this.nowDate = now.toLocaleDateString('en-IN', {
      timeZone: 'Asia/Kolkata',
      weekday: 'long',
      year: 'numeric',
      month: 'short',
      day: '2-digit'
    });
  }

  confirmLogout() {
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('user');

    this.router.navigate(['/auth/login']);
  }
}
