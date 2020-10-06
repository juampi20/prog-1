import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SensorComponent } from "./sensor/sensor.component"
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
            {
                path: 'sensor',
                data: { breadcrumb: 'Sensor' },
                children: [
                    {
                        path: '',
                        component: SensorComponent,
                    }
                ],
            },
            //Rutas de Usuario
            /* {
                path: 'user',
                data: { breadcrumb: 'User' },
                children: [
                    {
                        path: '',
                        component: UserComponent,
                    },
                ]
            }, */
        ],
    },
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
