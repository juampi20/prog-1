import { NgModule } from '@angular/core';
import { Routes, RouterModule, CanActivate } from '@angular/router';
// Importar componente de Sensor
import { SensorComponent } from "./sensor/sensor.component"
import { SensorAddComponent } from './sensor/sensor-add/sensor-add.component';
import { SensorEditComponent } from './sensor/sensor-edit/sensor-edit.component';
// Importar componente de User
import { UserComponent } from "./user/user.component"
// Importar componente de Login
import { LoginComponent } from './login/login.component';
//Importar servicio de proteccion de rutas
import { AuthGuardService as AuthGuard } from "./auth/auth-guard.service";

const routes: Routes = [
  // Home
  {
    path: '',
    redirectTo: '/',
    pathMatch: 'full',
    data: { breadcrumb: 'Home' },
  },
  // Principal
  {
    path: '',
    data: { breadcrumb: 'Home' },
    children: [
      //Rutas de Login
      {
        path: 'login',
        data: { breadcrumb: 'Login' },
        children: [
          {
            path: '',
            component: LoginComponent,
          },
        ],
      },
      //Rutas de Sensor
      {
        path: 'sensor',
        data: { breadcrumb: 'Sensor' },
        children: [
          {
            path: '',
            component: SensorComponent,
            //Asignar servicio de proteccion
            canActivate: [AuthGuard],
          },
          {
            path: 'add',
            component: SensorAddComponent,
            data: { breadcrumb: 'Add' },
            canActivate: [AuthGuard],
          },
          {
            path: 'edit/:id',
            component: SensorEditComponent,
            data: { breadcrumb: 'Edit' },
            canActivate: [AuthGuard],
          },
        ],
      },
      //Rutas de User
      {
        path: 'user',
        data: { breadcrumb: 'User' },
        children: [
          {
            path: '',
            component: UserComponent,
            canActivate: [AuthGuard],
          },
        ],
      },
    ],
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
