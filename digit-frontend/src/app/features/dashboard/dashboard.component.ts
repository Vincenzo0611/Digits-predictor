import { Component, OnInit } from '@angular/core';

import { CommonModule } from '@angular/common';

import { PredictionService }
from '../../core/services/prediction.service';

import { environment }
from '../../../environments/environment';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html'
})
export class DashboardComponent
implements OnInit {

  predictions: any[] = [];

  apiUrl = environment.apiUrl;

  constructor(
    private predictionService: PredictionService
  ) {}

  ngOnInit(): void {

    this.loadPredictions();
  }

  loadPredictions() {

    this.predictionService
      .getDashboard()
      .subscribe({

        next: (response) => {

          this.predictions = response;
        },

        error: (error) => {
          console.error(error);
        }
      });
  }

  deletePrediction(
    predictionId: number
  ) {

    this.predictionService
      .deletePrediction(
        predictionId
      )
      .subscribe({

        next: () => {

          this.predictions =
            this.predictions.filter(

              prediction =>
                prediction.id !==
                predictionId
            );
        },

        error: (error) => {

          console.error(error);
        }
      });
  }
}