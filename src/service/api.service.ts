import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  url = 'http://127.0.0.1:5000'

  create_user(dados:any): Promise<any> {
    return new Promise(resolve => {
      this.http.post(this.url + '/novo_cliente', dados).subscribe(
        data => {
          resolve(data)
        }
      )
    })
  }

  list_user(): Promise<any> {
    return new Promise(resolve => {
      this.http.get(this.url+'/listar_clientes').subscribe(
        data => {
          resolve(data)
        }
      )
    })
  }

  new_transfer(infos:any) {
    return new Promise(resolve => {
      this.http.post(this.url+'/nova', infos).subscribe(
        data => {
          resolve(data)
        }
      )
    })
  }

  delete_transfer(id:any) {
    return new Promise(resolve => {
      this.http.post(this.url+'/delete', id).subscribe(
        data => {
          resolve(data)
        }
      )
    })
  }

  list_transfer() {
    return new Promise(resolve => {
      this.http.get(this.url+'/listar').subscribe(
        data => {
          resolve(data)
        }
      )
    })
  }

}
