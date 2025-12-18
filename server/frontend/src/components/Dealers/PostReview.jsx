import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';


const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  let params = useParams();
  let id =params.id;
  let dealer_url = `/djangoapp/dealer/${id}`;
  let review_url = `/djangoapp/add_review`;
  let carmodels_url = `/djangoapp/get_cars`;

  const postreview = async ()=>{
    const username = sessionStorage.getItem("username");
    if (!username) {
      alert("Please login to post a review");
      window.location.href = window.location.origin + "/login";
      return;
    }

    let firstName = sessionStorage.getItem("firstname");
    let lastName = sessionStorage.getItem("lastname");
    let name = `${firstName || ""} ${lastName || ""}`.trim();
    if (!name || name.includes("null")) {
      name = username;
    }
    if(!model || review === "" || date === "" || year === "") {
      alert("All details are mandatory")
      return;
    }

    const [make_chosen, model_chosen] = model.split("|");
    if (!make_chosen || !model_chosen) {
      alert("Please choose a car make and model")
      return;
    }

    const jsoninput = JSON.stringify({
      "name": name,
      "dealership": id,
      "review": review,
      "purchase": true,
      "purchase_date": date,
      "car_make": make_chosen,
      "car_model": model_chosen,
      "car_year": year,
    });

    try {
      const res = await fetch(review_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "same-origin",
        body: jsoninput,
      });

      let json = null;
      try {
        json = await res.json();
      } catch {
        json = null;
      }

      if (!res.ok) {
        const msg = json?.error || json?.status || `Request failed (${res.status})`;
        alert(msg);
        return;
      }

      if (json?.status === 200) {
        window.location.href = window.location.origin+"/dealer/"+id;
        return;
      }

      alert(json?.error || "Could not post review");
    } catch (e) {
      alert("Network error posting review");
      console.error(e);
    }
  }
  const get_dealer = async ()=>{
    const res = await fetch(dealer_url, {
      method: "GET"
    });
    const retobj = await res.json();
    
    if(retobj.status === 200) {
      let dealerobjs = Array.from(retobj.dealer)
      if(dealerobjs.length > 0)
        setDealer(dealerobjs[0])
    }
  }

  const get_cars = async ()=>{
    const res = await fetch(carmodels_url, {
      method: "GET"
    });
    const retobj = await res.json();
    
    let carmodelsarr = Array.from(retobj.CarModels)
    setCarmodels(carmodelsarr)
  }
  useEffect(() => {
    get_dealer();
    get_cars();
  },[]);


  return (
    <div>
      <Header/>
      <div  style={{margin:"5%"}}>
      <h1 style={{color:"darkblue"}}>{dealer.full_name}</h1>
      <textarea id='review' cols='50' rows='7' onChange={(e) => setReview(e.target.value)}></textarea>
      <div className='input_field'>
      Purchase Date <input type="date" onChange={(e) => setDate(e.target.value)}/>
      </div>
      <div className='input_field'>
      Car Make 
        <select name="cars" id="cars" value={model} onChange={(e) => setModel(e.target.value)}>
        <option value="" disabled hidden>Choose Car Make and Model</option>
      {carmodels.map(carmodel => (
          <option value={carmodel.CarMake+"|"+carmodel.CarModel}>{carmodel.CarMake} {carmodel.CarModel}</option>
      ))}
      </select>        
      </div >

      <div className='input_field'>
        Car Year <input type="number" onChange={(e) => setYear(e.target.value)} max={2023} min={2015}/>
      </div>

      <div>
      <button className='postreview' onClick={postreview}>Post Review</button>
      </div>
    </div>
    </div>
  )
}
export default PostReview
