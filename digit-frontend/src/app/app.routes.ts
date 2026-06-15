import { Routes } from '@angular/router';

import { LoginComponent }
from './features/auth/login/login.component';

import { RegisterComponent }
from './features/auth/register/register.component';
import { DashboardComponent } from './features/dashboard/dashboard.component';
import { authGuard } from './core/guards/auth.guard';
import { PredictComponent } from './features/predict/predict.component';

export const routes: Routes = [

  {
    path: '',
    redirectTo: 'predict',
    pathMatch: 'full'
  },
  {
    path: 'login',
    component: LoginComponent
  },

  {
    path: 'register',
    component: RegisterComponent
  },
  {
    path: 'predict',
    component: PredictComponent,
    canActivate: [authGuard]
  },

  {
    path: 'dashboard',
    component: DashboardComponent,
    canActivate: [authGuard]
  },
  
];
