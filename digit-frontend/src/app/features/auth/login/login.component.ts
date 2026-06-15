import { Component } from '@angular/core';

import { FormsModule } from '@angular/forms';

import { AuthService } from '../../../core/services/auth.service';

import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './login.component.html'
})
export class LoginComponent {

  email = '';

  password = '';

  errorMessage = '';

  successMessage = '';

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  login() {
    
    this.errorMessage = '';

    this.successMessage = '';
    
    
    this.authService.login({
      email: this.email,
      password: this.password
    }).subscribe({

      next: (response) => {

        this.authService.saveToken(
          response.access_token
        );

        this.router.navigate(['/']);
      },

      error: (error) => {
        if (
          Array.isArray(error.error.detail)
        ) {

          this.errorMessage =
            error.error.detail[0].msg;

        } else if (
          typeof error.error.detail === 'string'
        ) {

          this.errorMessage =
            error.error.detail;

        } else {

          this.errorMessage =
            'Something went wrong';
        }
      }
    });
  }
}