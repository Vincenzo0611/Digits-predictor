import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../core/services/auth.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-register',
  imports: [RouterLink, FormsModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss'
})
export class RegisterComponent {

  email = '';

  password = '';

  errorMessage = '';

  successMessage = '';

  constructor(
      private authService: AuthService,
      private router: Router
  ) {}

  register() {
    
    this.errorMessage = '';

    this.successMessage = '';
    
    
    this.authService.register({
      email: this.email,
      password: this.password
    }).subscribe({

      next: (response) => {
        this.successMessage = 'Account created successfully. Now you can login.';
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
