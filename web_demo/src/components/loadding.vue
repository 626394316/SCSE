<template>
    <div class="loading">
      <div class="shape shape-4">
        <div class="shape-4-top"></div>
        <div class="shape-4-bottom"></div>
        <div class="shape-4-eye"></div>
      </div>
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>
</template>

<script>
export default {};
</script>


<style scoped>

.loading {
  /* width: 30px;
  height: 30px; */
  position: relative;
  display: flex;
  align-items: center;

}

.shape {
  width: 10px;
  height: 10px;
  position: absolute;
  border-radius: 50%;
  margin-left: 30px;
}

.shape-1 {
  background-color: #1875e5;
  left: -5px;
  animation: animationShape1 7s linear infinite;
}

.shape-2 {
  background-color: #c5523f;
  left: 15px;
  animation: animationShape2 7s linear infinite;
}

.shape-3 {
  background-color: #499255;
  left: 35px;
  animation: animationShape3 7s linear infinite;
}

.shape-4 {
  background-color: #f2b736;
  width: 30px;
  height: 30px;
  left: -40px;
  background-color: transparent !important;
  z-index: 2;
  animation: animationShape4 7s linear infinite;
}

.shape-4 > div {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.shape-4 .shape-4-top {
  position: absolute;
  top: 0;
  left: 0;
  background-color: #fbbc05;
  clip: rect(0 30px 15px 0);
  transform: rotate(-30deg);
  animation: animationShape4Top 0.4s ease infinite alternate;
}

.shape-4 .shape-4-bottom {
  position: absolute;
  top: 0;
  left: 0;
  background-color: #fbbc05;
  clip: rect(15px 30px 30px 0);
  transform: rotate(45deg);
  animation: animationShape4Bottom 0.4s ease infinite alternate;
}

.shape-4 .shape-4-eye {
  width: 5px;
  height: 5px;
  background-color: rgba(0, 0, 0, 0.8);
  border-radius: 50%;
  position: absolute;
  top: 5px;
  right: 10px;
}

@keyframes animationShape4Top {
  0% {
    transform: rotate(-30deg);
  }

  100% {
    transform: rotate(0);
  }
}

@keyframes animationShape4Bottom {
  0% {
    transform: rotate(45deg);
  }

  100% {
    transform: rotate(0);
  }
}

@keyframes animationShape1 {
  0% {
    opacity: 1;
  }

  17% {
    opacity: 1;
  }

  19% {
    opacity: 0;
  }

  30% {
    opacity: 0;
  }

  40% {
    opacity: 1;
  }

  85% {
    opacity: 1;
  }

  90% {
    opacity: 0;
  }

  95% {
    opacity: 0;
  }

  100% {
    opacity: 1;
  }
}

@keyframes animationShape2 {
  0% {
    opacity: 1;
  }

  20% {
    opacity: 1;
  }

  22% {
    opacity: 0;
  }

  35% {
    opacity: 0;
  }

  45% {
    opacity: 1;
  }

  75% {
    opacity: 1;
  }

  80% {
    opacity: 0;
  }

  90% {
    opacity: 0;
  }

  100% {
    opacity: 1;
  }
}

@keyframes animationShape3 {
  0% {
    opacity: 1;
  }

  27% {
    opacity: 1;
  }

  29% {
    opacity: 0;
  }

  40% {
    opacity: 0;
  }

  64% {
    opacity: 1;
  }

  65% {
    opacity: 1;
  }

  70% {
    opacity: 0;
  }

  80% {
    opacity: 0;
  }

  100% {
    opacity: 1;
  }
}

@keyframes animationShape4 {
  0% {
    left: -40px;
    transform: rotateY(0);
  }

  45% {
    left: 50px;
    transform: rotateY(0);
  }

  50% {
    left: 50px;
    transform: rotateY(180deg);
  }

  95% {
    left: -40px;
    transform: rotateY(180deg);
  }

  100% {
    left: -40px;
    transform: rotateY(0);
  }
}
</style>