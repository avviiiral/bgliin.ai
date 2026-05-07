import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CameraDetailsService } from './camera-detail.service';
import Chart from 'chart.js/auto';

@Component({
  selector: 'app-camera-detail',
  templateUrl: './camera-detail.component.html',
  styleUrls: ['./camera-detail.component.scss']
})
export class CameraDetailComponent implements OnInit {

  cameraId!: string;
  data: any;

  targetPerHour = 0;
  chartInstance: any;

  today = new Date();
  selectedMonth = this.today.getMonth() + 1;
  selectedYear = this.today.getFullYear();
  monthName = '';
  calendarDays: number[] = [];
  monthlyData: any[] = [];

  selectedDate = '';
  selectedDayData: any = null;

  constructor(
    private route: ActivatedRoute,
    private service: CameraDetailsService
  ) {}

  ngOnInit(): void {

    this.cameraId = this.route.snapshot.paramMap.get('id')!;
    this.selectedDate = this.route.snapshot.queryParamMap.get('date') || '';

    this.setMonthName();
    this.generateCalendar();
    this.loadMonthlyData();

    if (this.selectedDate) {
      this.loadSelectedDay();
    } else {
      this.loadCameraDetails();
    }
  }

  loadCameraDetails() {
    this.service.getCameraDetails(this.cameraId).subscribe({
      next: (res: any) => {
        this.data = res;

        this.prepareChart(
          res.hourly_output,
          res.target_per_hour,
          'time',
          'output',
          'chart1'
        );
      }
    });
  }

  loadSelectedDay() {
    this.service.getDayData(this.cameraId, this.selectedDate).subscribe({
      next: (res: any) => {

        this.selectedDayData = res;

        this.data = {
          ...this.data,
          name: res.name,
          efficiency: res.efficiency,
          output: res.total_output,
          target_per_hour: res.hourly?.[0]?.target || 0,
          date: res.date
        };

        this.prepareChart(
          res.hourly,
          res.hourly?.[0]?.target || 0,
          'hour',
          'count',
          'chart2'
        );
      }
    });
  }

  prepareChart(
    source: any[],
    target: number,
    labelKey: string,
    valueKey: string,
    canvasId: string
  ) {

    if (!source || source.length === 0) return;

    const labels = source.map(x => x[labelKey]);
    const data = source.map(x => x[valueKey]);

    this.targetPerHour = target;
    const max = Math.max(...data, target, 1);

    setTimeout(() => {

      if (this.chartInstance) {
        this.chartInstance.destroy();
      }

      const canvas = document.getElementById(canvasId) as HTMLCanvasElement;

      if (!canvas) return;

      this.chartInstance = new Chart(canvas, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            {
              label: 'Production',
              data,
              backgroundColor: data.map(v =>
                v >= target ? '#16a34a' : '#ef4444'
              ),
              borderRadius: 6,
              barThickness: 40
            },
            {
              type: 'line',
              label: 'Target',
              data: labels.map(() => target),
              borderColor: '#ef4444',
              borderDash: [6, 6],
              borderWidth: 2,
              pointRadius: 0
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            y: {
              beginAtZero: true,
              suggestedMax: Math.ceil(max / 20) * 20,
              ticks: { stepSize: 20 }
            },
            x: {
              grid: { display: false }
            }
          }
        }
      });

    }, 100);
  }

  setMonthName() {
    const date = new Date(this.selectedYear, this.selectedMonth - 1);
    this.monthName = date.toLocaleString('default', { month: 'long' });
  }

  generateCalendar() {
    const days = new Date(this.selectedYear, this.selectedMonth, 0).getDate();
    this.calendarDays = Array.from({ length: days }, (_, i) => i + 1);
  }

  loadMonthlyData() {
    this.service.getMonthlyHistory(
      this.cameraId,
      this.selectedYear,
      this.selectedMonth
    ).subscribe({
      next: (res) => this.monthlyData = res,
      error: () => this.monthlyData = []
    });
  }

  getMonthDay(day: number) {
    return this.monthlyData.find(x => x.day === day);
  }

  getColor(status: string): string {
    if (status === 'green') return '#16a34a';
    if (status === 'yellow') return '#ca8a04';
    return '#dc2626';
  }

  onDateClick(day: number) {
    const d = day.toString().padStart(2, '0');
    this.selectedDate =
      `${this.selectedYear}-${this.selectedMonth.toString().padStart(2, '0')}-${d}`;

    this.loadSelectedDay();
  }
}