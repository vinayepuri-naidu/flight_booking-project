import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { UserService } from '../user.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  source: string = '';
  destination: string = '';
  date: string = '';
  flights: any[] = [];
  bookings: any[] = [];
  loggedIn: boolean = false;

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit() {
    this.loggedIn = localStorage.getItem('loggedIn') === 'true';
    if (this.loggedIn) {
      this.getBookings();
    } else {
      this.router.navigate(['/login']);
    }
  }
  searchFlights() {
    if (!this.loggedIn) {
      alert('Please log in to search for flights');
      return;
    }

    this.http.get<any[]>('http://localhost:5000/flights', {
      params: {
        source: this.source,
        destination: this.destination,
        date: this.date
      }
    }).subscribe({
      next: (flights) => {
        console.log('Flights received:', flights);
        this.flights = flights;
        if (flights.length === 0) {
          alert('No flights available for the selected criteria');
        }
      },
      error: (error) => {
        console.error('Error fetching flights:', error);
        if (error.status === 400) {
          alert(error.error.message);
        } else if (error.status === 404) {
          alert(error.error.message);
        } else {
          alert('Error fetching flights. Please try again.');
        }
      }
    });
  }

  getBookings() {
    const userId = localStorage.getItem('userId');
    if (!userId) {
      console.error('User ID not found in local storage');
      return;
    }

    this.http.get<any[]>('http://localhost:5000/bookings', {
      params: { user_id: userId }
    }).subscribe({
      next: (bookings) => {
        console.log('Bookings received:', bookings);
        this.bookings = bookings;
      },
      error: (error) => {
        console.error('Error fetching bookings:', error);
        alert('Error fetching bookings. Please try again.');
      }
    });
  }

  bookFlight(flightId: number) {
    const userId = localStorage.getItem('userId');
    if (!userId) {
      console.error('User ID not found in local storage');
      return;
    }

    this.http.post<any>(`http://localhost:5000/book`, { user_id: userId, flight_id: flightId })
      .subscribe({
        next: (response) => {
          alert('Flight booked successfully');
          this.getBookings();
        },
        error: (error) => {
          console.error('Error booking flight:', error);
          
        }
      });
  }

  updateBooking(bookingId: number) {
    const flightNumber = prompt('Enter new flight number:');
    if (!flightNumber) {
      console.error('Flight number not provided');
      return;
    }
  
    console.log(`Updating booking with ID: ${bookingId} to new flight number: ${flightNumber}`);
  
    this.http.put<any>(`http://localhost:5000/bookings/${bookingId}`, { flight_number: flightNumber })
      .subscribe({
        next: (response) => {
          console.log('Booking update response:', response);
          alert('Booking updated successfully');
          this.getBookings();
        },
        error: (error) => {
          console.error('Error updating booking:', error);
          if (error.status === 400) {
            alert('Bad Request: ' + error.error.message);
          } else if (error.status === 404) {
            alert('Not Found: ' + error.error.message);
          } else {
            alert('Error updating booking. Please try again.');
          }
        }
      });
  }
  
  

  deleteBooking(bookingId: number) {
    this.http.delete<any>(`http://localhost:5000/bookings/${bookingId}`)
      .subscribe({
        next: (response) => {
          alert('Booking deleted successfully');
          this.getBookings();
        },
        error: (error) => {
          console.error('Error deleting booking:', error);
        }
      });
  }

  logout() {
    // Clear user data from local storage or session storage
    localStorage.removeItem('userId');
    localStorage.removeItem('loggedIn');
    
    // Navigate to the login page
    this.router.navigate(['/login']);
  }
}
