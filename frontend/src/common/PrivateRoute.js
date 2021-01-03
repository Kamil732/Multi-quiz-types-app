import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { Redirect, Route } from 'react-router-dom'

class PrivateRoute extends Component {
    static propTypes = {
        isAuthenticated: PropTypes.bool,
        userLoading: PropTypes.bool,
    }

    render() {
        if (this.props.userLoading === false && this.props.isAuthenticated === false) return <Redirect to="/login" />

        return <Route {...this.props} />
    }
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated,
    userLoading: state.auth.loading,
})

const mapDispatchToProps = {

}

export default connect(mapStateToProps, mapDispatchToProps)(PrivateRoute)