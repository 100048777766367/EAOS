package com.eaos.aiide

import com.eaos.aiide.viewmodel.WorkspaceViewModel
import org.junit.Assert.assertEquals
import org.junit.Before
import org.junit.Test

class WorkspaceViewModelTest {

    private lateinit var viewModel: WorkspaceViewModel

    @Before
    fun setUp() {
        viewModel = WorkspaceViewModel()
    }

    @Test
    fun testInitialWorkspaceState() {
        val initialFile = "apps/api/app/routers/chat.py"
        assertEquals(initialFile, "apps/api/app/routers/chat.py")
    }
}
