import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
//Importar servicio de autentificacion
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuardService implements CanActivate {

  constructor(public auth: AuthService, public router: Router) { }

  //Funcion que determina si una ruta puede o no navegarse
  canActivate(): boolean {
    //Verificar si el usuario esta autenticado
    if (!this.auth.isAuthenticated) {
      //Si no redireccionar a login
      this.router.navigate(['login']);
      //No se puede navegar
      return false;
    }
    //Se puede navegar
    return true;
  }
}
