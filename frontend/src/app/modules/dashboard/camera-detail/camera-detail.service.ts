import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class CameraDetailsService {

  BASE_URL = 'http://115.84.171.246:8000/api';

  constructor(private http: HttpClient) {}

  // ================= CAMERA DETAILS =================
  getCameraDetails(cameraId: string, date?: string) {

    let url =
      `${this.BASE_URL}/camera/${cameraId}/`;

    if (date) {
      url += `?date=${date}`;
    }

    return this.http.get(url);
  }

  // ================= MONTHLY HISTORY =================
  getMonthlyHistory(
    cameraId: string,
    year: number,
    month: number
  ) {

    return this.http.get<any[]>(
      `${this.BASE_URL}/monthly-history/${cameraId}/?year=${year}&month=${month}`
    );

  }

  // ================= DAY DETAILS =================
  getDayData(
    cameraId: string,
    date: string
  ) {

    return this.http.get<any>(
      `${this.BASE_URL}/camera/${cameraId}/day/?date=${date}`
    );

  }

}