import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthInterceptorService implements HttpInterceptor {

  constructor() { }

  //Funcion de intercepcion que se ejecutara cada vez que se haga una request HTTP
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    //Obtener el token
    const token = localStorage.getItem('token');
    //Si existe el token agregarlo a la request
    if (token) {
      const cloned = req.clone({
        headers: req.headers.set('Authorization', 'Bearer ' + token)
      });
      //Ejecutar request con la autorizacion agregada
      return next.handle(cloned);
    }
    else {
      //Ejecutar request 
      return next.handle(req);
    }
  }

}
