import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
//Importar servicio de Auth Interceptor
import { AuthInterceptorService } from './auth/auth-interceptor.service';
//Importar módulo de HTTP
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
//Importar módulo de formulario
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SensorComponent } from './sensor/sensor.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { UserComponent } from './user/user.component';
import { SensorDetailComponent } from './sensor/sensor-detail/sensor-detail.component';
import { SensorAddComponent } from './sensor/sensor-add/sensor-add.component';
import { SensorEditComponent } from './sensor/sensor-edit/sensor-edit.component';
import { LoginComponent } from './login/login.component';

@NgModule({
  declarations: [
    AppComponent,
    SensorComponent,
    UserComponent,
    SensorDetailComponent,
    SensorAddComponent,
    SensorEditComponent,
    LoginComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [
    //Cargar servicios de intercepción
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptorService,
      multi: true
    },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
