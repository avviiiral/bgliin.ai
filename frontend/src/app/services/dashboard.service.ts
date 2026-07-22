import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  API_URL = 'http://115.84.171.246:8000/api/dashboard/';

  constructor(private http: HttpClient) {}

  getMetrics() {
    return this.http.get<any>(this.API_URL);
  }
}