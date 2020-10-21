import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
// Importar componente de Sensor
import { SensorComponent } from "./sensor/sensor.component"
import { SensorAddComponent } from './sensor/sensor-add/sensor-add.component';
import { SensorEditComponent } from './sensor/sensor-edit/sensor-edit.component';
// Importar componente de User
import { UserComponent } from "./user/user.component"

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
      //Rutas de Sensor
      {
        path: 'sensor',
        data: { breadcrumb: 'Sensor' },
        children: [
          {
            path: '',
            component: SensorComponent,
          },
          {
            path: 'add',
            component: SensorAddComponent,
            data: { breadcrumb: 'Add' }
          },
          {
            path: 'edit/:id',
            component: SensorEditComponent,
            data: { breadcrumb: 'Edit' },
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
