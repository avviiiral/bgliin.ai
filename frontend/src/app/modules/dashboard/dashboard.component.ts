import { Component, OnInit, OnDestroy } from '@angular/core';
import { DashboardService } from '../../services/dashboard.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, OnDestroy {

  // 🔥 GLOBAL METRICS FROM BACKEND
  metrics: any = {
    efficiency: 0,
    output: 0,
    target: 0,
    active_stations: 0,
    total_stations: 0,
    per_station: {},
    per_station_targets: {}   // ✅ backend-driven targets
  };

  // 🔥 STATIONS CONFIG (NO TARGET HERE NOW)
  stations: any[] = [
    {
      id: 'cam10',
      name: 'BOBBIN STOPPER PRESSING',
      percent: '0%',
      status: '2',
      stream: 'http://localhost:8000/api/video_feed/cam10/'
    },
    {
      id: 'cam9',
      name: 'CORE FRAME RIVETTING',
      percent: '0%',
      status: '2',
      stream: 'http://localhost:8000/api/video_feed/cam9/'
    },
    {
      id: 'cam8',
      name: 'FRAME & MSPRING ASS',
      percent: '0%',
      status: '2',
      stream: 'http://localhost:8000/api/video_feed/cam8/'
    },
    {
      id: 'cam7',
      name: 'FRAME & BASE ASS',
      percent: '0%',
      status: '2',
      stream: 'http://localhost:8000/api/video_feed/cam7/'
    },
    {
      id: 'cam6',
      name: 'WIRE ROUTING',
      percent: '0%',
      status: '2',
      stream: 'http://localhost:8000/api/video_feed/cam6/'
    },
    {
      id: 'cam5',
      name: 'COMMON CRIMPING',
      percent: '0%',
      status: '2',
      stream: 'http://localhost:8000/api/video_feed/cam5/'
    },
    {
      id: 'cam4',
      name: 'FRAME CRIPMING',
      percent: '0%',
      status: '2',
      stream: 'http://localhost:8000/api/video_feed/cam4/'
    },
    {
      id: 'cam3',
      name: 'COIL SOLDRING',
      percent: '0%',
      status: '2',
      stream: 'http://localhost:8000/api/video_feed/cam3/'
    },
    {
      id: 'cam2',
      name: 'MIDDLE TESTING',
      percent: '0%',
      status: '2',
      stream: 'http://localhost:8000/api/video_feed/cam2/'
    },
    {
      id: 'cam1',
      name: 'AIR WASHING',
      percent: '0%',
      status: '2',
      stream: 'http://localhost:8000/api/video_feed/cam1/'
    }
  ];

  private intervalId: any;

  constructor(
    private dashboardService: DashboardService,
    private router: Router
  ) {}

  // ==============================
  // INIT
  // ==============================
  ngOnInit(): void {
    this.loadMetrics();

    this.intervalId = setInterval(() => {
      this.loadMetrics();
    }, 2000);
  }

  ngOnDestroy(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }

  // ==============================
  // NAVIGATION
  // ==============================
  openCamera(id: string) {
    this.router.navigateByUrl('/dashboard/camera/' + id);
  }

  openStation(item: any) {
    this.router.navigate(['/dashboard/station', item.id]);
  }

  // ==============================
  // API CALL
  // ==============================
  loadMetrics(): void {
    this.dashboardService.getMetrics().subscribe({
      next: (res: any) => {
        this.metrics = res;
        this.updateStationData();
      },
      error: (err: any) => {
        console.error('Dashboard API error:', err);
      }
    });
  }

  // ==============================
  // UPDATE UI FROM BACKEND
  // ==============================
  updateStationData(): void {
    if (!this.metrics?.per_station || !this.metrics?.per_station_targets) return;

    this.stations.forEach(station => {
      const count = this.metrics.per_station[station.id] || 0;

      // ✅ FULLY BACKEND-DRIVEN TARGET
      const target = this.metrics.per_station_targets[station.id] || 1;

      const efficiency = (count / target) * 100;

      station.percent = efficiency.toFixed(1) + '%';

      if (efficiency >= 80) {
        station.status = '0';
      } else if (efficiency >= 70) {
        station.status = '1';
      } else {
        station.status = '2';
      }
    });
  }
}