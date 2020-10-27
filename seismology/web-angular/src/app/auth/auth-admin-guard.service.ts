import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
//Importar servicio de autentificacion
import { AuthService } from './auth.service';
//Importar libreria jwt
import jwt_decode from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})
export class AuthAdminGuardService implements CanActivate {

  constructor(public auth: AuthService, public router: Router) { }

  //Funcion que determina si una ruta puede o no navegarse
  canActivate(): boolean {
    //Verificar si el usuario esta autenticado
    if (this.auth.isAuthenticated) {
      //Obtener el token
      const token = localStorage.getItem('token');
      const token_decode = jwt_decode(token);
      console.log(token_decode);
      if (token_decode.user_claims.admin) {
        //Se puede navegar
        return true;
      }
    }
    //Si no redireccionar a login
    this.router.navigate(['login']);
    //No se puede navegar
    return false;
  }
}
