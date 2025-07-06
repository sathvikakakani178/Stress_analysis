# Deployment Guide - Medical Stress Detection System

## Quick Start

### Method 1: Streamlit Cloud (Recommended)

1. **Upload to GitHub:**
   - Create a new repository on GitHub
   - Upload all files from the deployment_package folder
   - Ensure all files are in the root directory

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Set main file path: `app.py`
   - Click "Deploy"

### Method 2: Local Development

1. **Install Python 3.9+**
   - Download from [python.org](https://python.org)

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Application:**
   ```bash
   streamlit run app.py
   ```

4. **Access Application:**
   - Open browser to `http://localhost:8501`

### Method 3: Docker Deployment

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app
   COPY . .

   RUN pip install -r requirements.txt

   EXPOSE 8501

   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and Run:**
   ```bash
   docker build -t medical-stress-app .
   docker run -p 8501:8501 medical-stress-app
   ```

## Configuration

### Streamlit Configuration

The `.streamlit/config.toml` file contains:
- Server settings (port, address)
- Theme configuration
- UI preferences

### Environment Variables

No additional environment variables required for basic operation.

## Troubleshooting

### Common Issues

1. **Import Errors:**
   - Ensure all Python files are in the same directory
   - Check requirements.txt installation

2. **Port Issues:**
   - Change port in config.toml if 8501 is busy
   - Use `--server.port` flag to override

3. **Memory Issues:**
   - Reduce n_estimators in RandomForest if needed
   - Clear browser cache

### Performance Optimization

1. **Caching:**
   - System uses @st.cache_resource for model loading
   - Data is cached automatically

2. **Resource Usage:**
   - Model training is simulated for demo purposes
   - Real deployment would use pre-trained models

## Security Considerations

1. **Data Privacy:**
   - No patient data is stored permanently
   - Session data is browser-local only

2. **Medical Compliance:**
   - System includes medical disclaimers
   - Not intended for actual medical diagnosis

## Monitoring

### Health Checks

The application includes:
- System status indicators
- Session monitoring
- Parameter validation

### Logging

- Streamlit provides built-in logging
- Custom logging can be added as needed

## Support

For deployment issues:
1. Check Streamlit documentation
2. Verify all files are included
3. Ensure Python version compatibility
4. Review error logs for specific issues

## Production Considerations

### Before Production Use:

1. **Medical Validation:**
   - Validate with medical professionals
   - Ensure compliance with healthcare regulations

2. **Performance Testing:**
   - Test with multiple concurrent users
   - Validate on different devices/browsers

3. **Security Review:**
   - Implement proper authentication if needed
   - Review data handling practices

4. **Monitoring:**
   - Set up application monitoring
   - Configure error tracking

### Scaling

For high-traffic deployment:
1. Consider using Streamlit Cloud's commercial tier
2. Implement database for persistent storage
3. Add load balancing if needed
4. Monitor resource usage and optimize