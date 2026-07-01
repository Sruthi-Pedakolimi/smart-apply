import { useState } from "react"
import "./index.css"

const SmartApply = () => {
  const [file, updateFile] = useState("")
  const [job_summary, updateSummary] = useState("")
  const [cover_letter, updateCoverLetter] = useState("")
  const [ats_score, updateATSScore] = useState("")
  const [error, updateError] = useState("")
  const [isLoading, updateIsLoading] = useState(false)

  const handleFileChange = (event) => {
        updateFile(event.target.files[0])
  }

  const handleJobSummaryChange = (event) => {
        updateSummary(event.target.value)
  }

  const handleSubmit = async (event) =>{

    if (job_summary.trim() == ""){
      updateError("Please fill job summary")
      return
    }
    if (!file){
       updateError("Please Upload file")
      return
    }

    const url = "http://localhost:8000/info"
    const formData = new FormData();
    formData.append("file", file);
    formData.append("job", job_summary);
    updateError("")
    updateIsLoading(true)
    const response = await fetch(url, {
      method: 'POST',
      body: formData
    })
    if (!response.ok){
      updateIsLoading(false)
      return
    }
 
    const data = await response.json()
    updateIsLoading(false)
    updateCoverLetter(data.cover_letter)
    updateATSScore(data.ats_score)
  }

  const formatOutput = () => {
      return (
        <>
          <label className="label-heading">Output</label>
          <p className="ats-score">ATS Score: {ats_score}</p>
          <p className="cover-letter">{cover_letter}</p>
       </> 
      )
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
       <div className="output-container">
        {isLoading && <p className="generating">Generating.....</p>}
        {error && <p className="error">{error}</p>} 
        {cover_letter && formatOutput()} 
        </div>  
    </div>
    </div>

  )
}


export default SmartApply