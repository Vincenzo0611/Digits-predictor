import { Component } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {

  constructor(
    private router: Router
  ) {}

  isLoggedIn(): boolean {

    return !!localStorage.getItem(
      'token'
    );
  }

  logout() {

    localStorage.removeItem(
      'token'
    );

    this.router.navigate([
      '/login'
    ]);
  }
}
