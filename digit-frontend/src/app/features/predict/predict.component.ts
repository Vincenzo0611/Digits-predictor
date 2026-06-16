import { Component } from '@angular/core';

import { CommonModule } from '@angular/common';

import { FormsModule } from '@angular/forms';

import { PredictionService }
from '../../core/services/prediction.service';

import { environment }
from '../../../environments/environment';

@Component({
  selector: 'app-predict',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './predict.component.html'
})
export class PredictComponent {

  isLoading = false;

  selectedFile!: File;

  predictionResult: any = null;

  correctDigit = '';

  processedImageUrl = '';

  feedbackMessage = '';

  showHelpModal = false;

  apiUrl = environment.apiUrl;

  feedbackChoice: 'correct' | 'wrong' | null = null;

  selectedDigit: number | null = null;

  constructor(
    private predictionService: PredictionService
  ) {}

  onFileSelected(event: any) {

    this.selectedFile = event.target.files[0];
  }

  uploadImage() {

    if (!this.selectedFile) {
      return;
    }
    this.isLoading = true;
    this.predictionService
      .predict(this.selectedFile)
      .subscribe({

        next: (response) => {
          this.predictionResult = response;

          this.processedImageUrl = response.processed_image_url;

          this.isLoading = false;
        },

        error: (error) => {
          this.isLoading = false;
          console.error(error);
        }
      });
  }

  sendCorrectFeedback() {

    this.predictionService
      .sendFeedback({
        prediction_id:
          this.predictionResult.prediction_id,

        is_correct: true, 
        correct_digit: Number(10)
      })
      .subscribe(() => {

        this.feedbackMessage = 'Feedback saved';
        this.feedbackChoice = null;
        this.selectedDigit = null;
        setTimeout(() => {

          this.feedbackMessage = '';

        }, 3000);
        
        this.resetPrediction();
      });
  }

  sendWrongFeedback(correctDigit: number) {

    this.predictionService
      .sendFeedback({

        prediction_id:
          this.predictionResult.prediction_id,

        is_correct: false,

        correct_digit: correctDigit

      })
      .subscribe(() => {

        this.feedbackMessage = 'Feedback saved';
        this.feedbackChoice = null;
        this.selectedDigit = null;
        setTimeout(() => {

          this.feedbackMessage = '';

        }, 3000);

        this.resetPrediction();
      });
  }

  resetPrediction() {

    this.predictionResult = null;

    this.correctDigit = '';

    this.processedImageUrl = '';
  }

  markCorrect() {

    this.feedbackChoice = 'correct';

    this.sendCorrectFeedback();
  }

  markWrong() {

    this.feedbackChoice = 'wrong';
  }

  selectDigit(
    digit: number
  ) {

    this.selectedDigit = digit;
  }

  submitWrongFeedback() {

    if (
      this.selectedDigit === null
    ) {

      return;
    }

    this.sendWrongFeedback(
      this.selectedDigit
    );
  }
  openHelpModal() {

    this.showHelpModal = true;
  }

  closeHelpModal() {

    this.showHelpModal = false;
  }
}