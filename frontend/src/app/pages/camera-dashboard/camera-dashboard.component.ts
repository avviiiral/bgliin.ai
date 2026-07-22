import { Component, OnInit, AfterViewInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-camera-dashboard',
  templateUrl: './camera-dashboard.component.html',
  styleUrls: ['./camera-dashboard.component.scss']
})
export class CameraDashboardComponent implements OnInit, AfterViewInit {

  rawData: any[] = [];
  hourlyData: number[] = [];
  labels: string[] = [];
  station: string = '';

  totalOutput = 0;
  efficiency = 0;
  pph = 0;

  constructor(
    private http: HttpClient,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    this.station = this.route.snapshot.queryParams['station'] || 'BOBBIN PRESSING';

    this.http.get<any[]>('http://115.84.171.246:8000/api/dashboard-data/')
      .subscribe(res => {
        this.rawData = res;
        this.prepareData();
      });
  }

  ngAfterViewInit() {
    setTimeout(() => {
      this.renderCharts();
    }, 500);
  }

  prepareData() {
    this.hourlyData = this.rawData.map(d => Number(d[this.station] || 0));
    this.labels = this.rawData.map(d => d['Time Slot']);

    this.totalOutput = this.hourlyData.reduce((a, b) => a + b, 0);

    const hours = this.hourlyData.length || 1;
    this.pph = this.totalOutput / hours;

    const targetPerHour = 400;
    this.efficiency = (this.totalOutput / (targetPerHour * hours)) * 100;
  }

  renderCharts() {
    // Hourly Bar Chart
    
  }
}