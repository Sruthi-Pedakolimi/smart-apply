import { useState } from "react"


const SmartApply = () => {
  const [file, updateFile] = useState("")
  const [job_summary, updateSummary] = useState("")
  const [cover_letter, updateCoverLetter] = useState("")
  const [ats_score, updateATSScore] = useState("")

  const handleFileChange = (event) => {
        updateFile(event.target.files[0])
  }

  const handleJobSummaryChange = (event) => {
      if (event.target.value != "") {
        updateSummary(event.target.value)
      }
  }

  const handleSubmit = async (event) =>{
    console.log("submitted successfully")
    const url = "http://localhost:8000/info"
    const formData = new FormData();
    formData.append("file", file);
    formData.append("job", job_summary);

    const response = await fetch(url, {
      method: 'POST',
      body: formData
    })
    const data = await response.json()
    updateCoverLetter(data.cover_letter)
    updateATSScore(data.ats_score)
  }

  return (
    <div className="app-container">    
      <div className="main-container">
       <h1 className="app-heading">Smart Apply</h1>
       <div className="file-input-container">
          <label className="label-heading">Upload file</label>
          <input type="file" onChange={handleFileChange} className="file-input"/>
       </div>
       <div className="job-summary-container">
          <label className="label-heading">Job Description</label>
          <textarea onChange={handleJobSummaryChange} className="text-input"/>
       </div>
       <div className="submit-container">
       <button onClick={handleSubmit} className="submit-btn">
          Submit
       </button>
       </div>
       <div>
          <label className="label-heading">Output</label>
          <p>{ats_score}</p>
          <p>{cover_letter}</p>
       </div>
    </div>
    </div>

  )
}


export default SmartApply