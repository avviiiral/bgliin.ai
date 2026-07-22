import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Camera {
  name: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private API = 'http://115.84.171.246:8000';

  constructor(private http: HttpClient) {}

  // ✅ Dashboard
  getCameras(): Observable<Record<string, Camera>> {
    return this.http.get<Record<string, Camera>>(`${this.API}/cameras`);
  }

  // ✅ Camera Live Feed
  getCameraFeed(id: string): string {
    return `${this.API}/camera/${id}`;
  }

  // ✅ Camera Detail Page (IMPORTANT - KEEP THIS)
  getHourlyCounts(id: string): Observable<any> {
    return this.http.get(`${this.API}/counts/hourly/${id}`);
  }

}