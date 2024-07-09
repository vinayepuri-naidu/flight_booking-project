import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string = '';
  password: string = '';

  constructor(private http: HttpClient, private router: Router) {}

  login() {
    this.http.post<any>('http://localhost:5000/login', { username: this.username, password: this.password })
      .subscribe({
        next: (response) => {
          alert('Login successful');
          localStorage.setItem('userId', response.userId);
          localStorage.setItem('loggedIn', 'true');
          this.router.navigate(['/dashboard']);
        },
        error: (error) => {
          console.error('Error logging in:', error);
          alert('Invalid username or password');
        }
      });
  }
}
