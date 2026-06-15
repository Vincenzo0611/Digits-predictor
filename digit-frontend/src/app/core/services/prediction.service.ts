import { Injectable } from '@angular/core';

import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PredictionService {

  private apiUrl = environment.apiUrl;

  constructor(
    private http: HttpClient
  ) {}

  predict(file: File): Observable<any> {

    const formData = new FormData();

    formData.append('file', file);

    return this.http.post(
      `${this.apiUrl}/predict/`,
      formData
    );
  }

  sendFeedback(data: any): Observable<any> {

    return this.http.post(
      `${this.apiUrl}/feedback/`,
      data
    );
  }

  getDashboard(): Observable<any> {

    return this.http.get(
      `${this.apiUrl}/dashboard/`
    );
  }

  deletePrediction(predictionId: number) {

    return this.http.delete(

      `${this.apiUrl}/dashboard/${predictionId}`

    );
  }
}

