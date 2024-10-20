from django.shortcuts import render, redirect
from django.http import HttpResponse

# Global dictionary to store which segments are revealed
revealed_segments = {f'segment_{i}': False for i in range(1, 26)}
revealed_segments['segment_0'] = False  # Middle segment (QR for the whole image)

# List of specific segments required for segment_0 to be revealed
required_segments = [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24]

def large_screen(request):
    """Render the main screen with QR codes or image segments."""
    context = {
        'segments': revealed_segments,  # Segments state
    }
    return render(request, 'large_screen.html', context)

def reveal(request, segment):
    """Handle reveal logic for a particular segment."""
    if segment in revealed_segments or segment == 'segment_25':  # Allow 'segment_25' without being in the dictionary
        if request.method == 'POST':  # Handle reveal button click
            if segment == 'segment_0':
                # Check if the specific segments are revealed
                required_segments_revealed = all(revealed_segments[f'segment_{i}'] for i in required_segments)
                
                if required_segments_revealed:
                    revealed_segments['segment_0'] = True  # Reveal the middle image
                else:
                    return render(request, 'error.html')
            
            elif segment == 'segment_25':
                # If segment_25 is clicked, just redirect to the success page without revealing anything
                return redirect('success_page')

            revealed_segments[segment] = True  # Mark the segment as revealed (for all other segments)
            return redirect('success_page')  # Redirect back to the main page
    else:
        return HttpResponse("Invalid segment", status=404)

    return render(request, 'reveal.html', {'segment': segment})

def success_page(request):
    """Render the success page with the image."""
    return render(request, 'success.html')

def qr_code_status(request):
    """Render a page displaying the status of all QR codes."""
    context = {
        'segments': revealed_segments,  # Pass the revealed_segments dictionary to the template
    }
    return render(request, 'qr_code_status.html', context)
    
def reset_revealed_segments(request):
    """Reset all revealed segments to False."""
    for key in revealed_segments.keys():
        revealed_segments[key] = False
    return redirect('qr_code_status')  # Redirect back to the QR Code Status page
