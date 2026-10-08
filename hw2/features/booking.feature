Feature: Movie seat booking
    As a moviegoer
    I want to browse movies and book a seat
    So that I can attend a showing

    Background:
        Given a movie "Dune" with 1 available seat "A1"
        And I am logged in as "alice"

    Scenario: Viewing the movie list
        When I visit the movie list page
        Then I should see "Dune" on the page

    Scenario: Booking an available seat
        When I book seat "A1" for "Dune"
        Then the seat "A1" should be marked as booked
        And my booking history should contain "Dune"

    Scenario: Seat is unavailable after being booked
        Given seat "A1" for "Dune" is already booked
        When I visit the seat booking page for "Dune"
        Then I should not be able to select seat "A1"
