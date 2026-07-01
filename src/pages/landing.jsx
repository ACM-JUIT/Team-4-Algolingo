import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import Features from "../components/Features";
import Stats from "../components/Stats";
import Roadmap from "../components/Roadmap";
import Testimonials from "../components/Testimonials";
import FAQ from "../components/FAQ";
import Footer from "../components/Footer";

function Landing() {
  return (
    <>
      <Navbar />
      <Hero />
      <Features />
      <Stats />
      <Roadmap />
      <Testimonials />
      <FAQ />
      <Footer />
    </>
  );
}

export default Landing;