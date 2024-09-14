function countdownTo(targetDate) {
    const targetTime = new Date(targetDate).getTime();
  
    if (isNaN(targetTime)) {
      throw new Error("تاریخ وارد شده نامعتبر است");
    }
  
    function displayTimeRemaining() {
      const now = new Date().getTime();
      const distance = targetTime - now;
  
      if (distance < 0) {
        clearInterval(interval); 
        return;
      }
  
      const days = Math.floor(distance / (1000 * 60 * 60 * 24));
      const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((distance % (1000 * 60)) / 1000);
  

      days_elms = document.querySelector('.brz-countdown2__days div');
      hours_elm = document.querySelector('.brz-countdown2__hours div');
      minutes_elm = document.querySelector('.brz-countdown2__minutes div');
      seconds_elm = document.querySelector('.brz-countdown2__seconds div');
      
      days_elms.innerHTML = days;
      hours_elm.innerHTML = hours;
      minutes_elm.innerHTML = minutes;
      seconds_elm.innerHTML = seconds;

    }
  
    const interval = setInterval(displayTimeRemaining, 1000);
  }
  

  try {
    countdownTo(targetDate);
  } catch (error) {
    console.error(error);
  }